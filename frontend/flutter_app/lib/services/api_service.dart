import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auth_service.dart';

class ApiService {
  final AuthService authService;
  static const String baseUrl = 'http://localhost:8000';
  
  ApiService(this.authService);
  
  // Career Service
  Future<List<dynamic>> getCareerGoals() async {
    final response = await http.get(
      Uri.parse('$baseUrl/career/goals'),
      headers: authService.getAuthHeaders(),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load career goals');
  }
  
  Future<Map<String, dynamic>> createCareerGoal(Map<String, dynamic> goal) async {
    final response = await http.post(
      Uri.parse('$baseUrl/career/goals'),
      headers: authService.getAuthHeaders(),
      body: json.encode(goal),
    );
    
    if (response.statusCode == 201) {
      return json.decode(response.body);
    }
    throw Exception('Failed to create career goal');
  }
  
  // Health Service
  Future<List<dynamic>> getHealthRecords({String? recordType, int days = 30}) async {
    final uri = Uri.parse('$baseUrl/health/records')
        .replace(queryParameters: {
          if (recordType != null) 'record_type': recordType,
          'days': days.toString(),
        });
    
    final response = await http.get(
      uri,
      headers: authService.getAuthHeaders(),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load health records');
  }
  
  Future<Map<String, dynamic>> createHealthRecord(Map<String, dynamic> record) async {
    final response = await http.post(
      Uri.parse('$baseUrl/health/records'),
      headers: authService.getAuthHeaders(),
      body: json.encode(record),
    );
    
    if (response.statusCode == 201) {
      return json.decode(response.body);
    }
    throw Exception('Failed to create health record');
  }
  
  // Finance Service
  Future<List<dynamic>> getTransactions({String? transactionType, int days = 30}) async {
    final uri = Uri.parse('$baseUrl/finance/transactions')
        .replace(queryParameters: {
          if (transactionType != null) 'transaction_type': transactionType,
          'days': days.toString(),
        });
    
    final response = await http.get(
      uri,
      headers: authService.getAuthHeaders(),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load transactions');
  }
  
  Future<Map<String, dynamic>> createTransaction(Map<String, dynamic> transaction) async {
    final response = await http.post(
      Uri.parse('$baseUrl/finance/transactions'),
      headers: authService.getAuthHeaders(),
      body: json.encode(transaction),
    );
    
    if (response.statusCode == 201) {
      return json.decode(response.body);
    }
    throw Exception('Failed to create transaction');
  }
  
  Future<Map<String, dynamic>> getFinancialSummary() async {
    final response = await http.get(
      Uri.parse('$baseUrl/finance/analytics/summary'),
      headers: authService.getAuthHeaders(),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load financial summary');
  }
  
  // Recommendations
  Future<List<dynamic>> getRecommendations(String type) async {
    final response = await http.get(
      Uri.parse('$baseUrl/$type/recommendations'),
      headers: authService.getAuthHeaders(),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Failed to load recommendations');
  }
}

